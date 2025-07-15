import { combineReducers, configureStore, ThunkAction } from '@reduxjs/toolkit';
import configReducer from './reducers/configReducer';
import { ConfigAction, ConfigState } from '../Services/models/configModels';

export interface State {
  configReducer: ConfigState;
}

const rootReducer = combineReducers({
  configReducer,
});

export const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      immutableCheck: { warnAfter: 250 },
      serializableCheck: { warnAfter: 250 },
    }),
});

export type RootState = ReturnType<typeof rootReducer>;

export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  ConfigAction
>;

export type AppDispatch = typeof store.dispatch & ((action: AppThunk) => ReturnType<AppThunk>);

export default store;
