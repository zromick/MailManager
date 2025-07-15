import { ConfigDataKeys, ConfigState } from '../models/configModels';
import { State } from '../../Store/Store';

// The purpose of this file is to keep pieces of state easily changeable and reference-able throughout the app.

// Config State

export type GetAllMailItemsDataType = ConfigState['api']['data'][ConfigDataKeys.FETCH_GET_ALL_MAIL_ITEMS];
export const getAllMailItemsDataState = (state: State) => state.configReducer.api?.data?.fetchGetAllMailItems;

export type GetMailItemDataType = ConfigState['api']['data'][ConfigDataKeys.FETCH_GET_MAIL_ITEMS];
export const GetMailItemDataState = (state: State) => state.configReducer.api?.data?.fetchGetMailItems;

export type FlagsType = ConfigState['api']['flags']
export const flagsState = (state: State) => state.configReducer.api?.flags;

export type PostMailItemDataType = ConfigState['api']['data'][ConfigDataKeys.FETCH_PATCH_MAIL_ITEMS];
export const PostMailItemDataState = (state: State) => state.configReducer.api?.data?.fetchPostMailItems;

export type PatchMailItemDataType = ConfigState['api']['data'][ConfigDataKeys.FETCH_POST_MAIL_ITEMS];
export const PatchMailItemDataState = (state: State) => state.configReducer.api?.data?.fetchPatchMailItems;
