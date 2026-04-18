import { useReducer, useCallback } from 'react';
import { fetchEventSource } from '@microsoft/fetch-event-source';
import { PipelineState, PipelineAction, PipelineStage } from '../types/pipeline';

const initialState: PipelineState = {
  stage: 'idle',
  progress: 0,
  logs: [],
  results: {},
};

function pipelineReducer(state: PipelineState, action: PipelineAction): PipelineState {
  switch (action.type) {
    case 'START':
      return { ...initialState, stage: 'classify', logs: ['Initiating pipeline...'] };
    case 'UPDATE_PROGRESS':
      return { ...state, progress: action.payload };
    case 'ADD_LOG':
      return { ...state, logs: [...state.logs, action.payload] };
    case 'SET_RESULT':
      const nextStageMap: Record<string, PipelineStage> = {
        classification: 'triage',
        triage: 'rag',
        rag: 'resolve',
        resolution: 'judge',
        judge: 'complete'
      };
      return {
        ...state,
        results: { ...state.results, [action.payload.key]: action.payload.data },
        stage: nextStageMap[action.payload.key] || state.stage
      };
    case 'COMPLETE':
      return { ...state, stage: 'complete', progress: 1 };
    case 'ERROR':
      return { ...state, stage: 'error', error: action.payload };
    case 'RESET':
      return initialState;
    default:
      return state;
  }
}

export function usePipeline() {
  const [state, dispatch] = useReducer(pipelineReducer, initialState);

  const startPipeline = useCallback(async (title: string, description: string) => {
    dispatch({ type: 'START' });

    const ctrl = new AbortController();
    
    try {
      await fetchEventSource('/api/pipeline/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description }),
        signal: ctrl.signal,
        onmessage(msg) {
          if (msg.event === 'status') {
            const data = JSON.parse(msg.data);
            if (data.log) dispatch({ type: 'ADD_LOG', payload: data.log });
            if (data.progress) dispatch({ type: 'UPDATE_PROGRESS', payload: data.progress });
          } else if (msg.event === 'result') {
            const data = JSON.parse(msg.data);
            dispatch({ type: 'SET_RESULT', payload: { key: data.type, data: data.payload } });
          } else if (msg.event === 'done') {
            dispatch({ type: 'COMPLETE' });
          }
        },
        onerror(err) {
          dispatch({ type: 'ERROR', payload: 'Connection lost. Retrying...' });
          throw err;
        }
      });
    } catch (err) {
      if (err instanceof Error && err.name !== 'AbortError') {
        dispatch({ type: 'ERROR', payload: err.message });
      }
    }

    return () => ctrl.abort();
  }, []);

  return { state, startPipeline, reset: () => dispatch({ type: 'RESET' }) };
}
