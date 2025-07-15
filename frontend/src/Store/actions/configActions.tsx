import { Dispatch } from 'react';
import {
  fetchGetAllMailItems,
  fetchGetMailItem,
  fetchPatchMailItem,
  fetchPostMailItem,
} from '../../Services/api/configApi';
import {
  ConfigAction, ConfigActionOptions, Data,
  ConfigFlags, ConfigFlagAction, ConfigDataAction,
  ConfigDataKeys, FetchPostMailItemsParams, FetchGetAllMailItemsParams,
  FetchGetMailItemsParams, FetchPatchMailItemsParams,
  GetAllMailItemsResponse, MailItemResponse
} from '../../Services/models/configModels';


export const setConfigFlagActionCreator = (update: ConfigFlags):ConfigFlagAction => ({
  type: ConfigActionOptions.SET_CONFIG_API_FLAG,
  payload: update,
});

export const setConfigDataActionCreator = (update: Data):ConfigDataAction => ({
  type: ConfigActionOptions.SET_CONFIG_API_DATA,
  payload: update,
});

export const fetchGetMailItemActionCreator = (fetchParams:FetchGetMailItemsParams) => async (dispatch:Dispatch<ConfigAction>) => {
  const flags = ConfigFlags.FETCH_GET_MAIL_ITEMS;
  const dataKey = ConfigDataKeys.FETCH_GET_MAIL_ITEMS;
  dispatch(setConfigFlagActionCreator(flags));
  try {
    const response = await fetchGetMailItem(fetchParams);
    const fetchedData:MailItemResponse = await response.json();
    dispatch(setConfigFlagActionCreator(flags));
    dispatch(setConfigDataActionCreator({ [dataKey]: fetchedData }));
  } catch {
    // To-Do: Handle Errors
    dispatch(setConfigFlagActionCreator(flags));
  }
};

export const fetchGetAllMailItemsActionCreator = (fetchParams:FetchGetAllMailItemsParams) => async (dispatch:Dispatch<ConfigAction>) => {
  const flags = ConfigFlags.FETCH_GET_ALL_MAIL_ITEMS;
  const dataKey = ConfigDataKeys.FETCH_GET_ALL_MAIL_ITEMS;
  dispatch(setConfigFlagActionCreator(flags));
  try {
    const response = await fetchGetAllMailItems(fetchParams);
    const fetchedData:GetAllMailItemsResponse = await response.json();
    dispatch(setConfigFlagActionCreator(flags));
    dispatch(setConfigDataActionCreator({ [dataKey]: fetchedData }));
  } catch {
    // To-Do: Handle Errors
    dispatch(setConfigFlagActionCreator(flags));
  }
};

export const fetchPostMailItemActionCreator = (fetchParams:FetchPostMailItemsParams) => async (dispatch:Dispatch<ConfigAction>) => {
  const flags = ConfigFlags.FETCH_POST_MAIL_ITEMS;
  const dataKey = ConfigDataKeys.FETCH_POST_MAIL_ITEMS;
  dispatch(setConfigFlagActionCreator(flags));
  try {
    const response = await fetchPostMailItem(fetchParams);
    const fetchedData:MailItemResponse = await response.json();
    dispatch(setConfigFlagActionCreator(flags));
    dispatch(setConfigDataActionCreator({ [dataKey]: fetchedData }));
  } catch {
    // To-Do: Handle Errors
    dispatch(setConfigFlagActionCreator(flags));
  }
};

export const fetchPatchMailItemActionCreator = (fetchParams:FetchPatchMailItemsParams) => async (dispatch:Dispatch<ConfigAction>) => {
  const flags = ConfigFlags.FETCH_PATCH_MAIL_ITEMS;
  const dataKey = ConfigDataKeys.FETCH_PATCH_MAIL_ITEMS;
  dispatch(setConfigFlagActionCreator(flags));

  try {
    const response = await fetchPatchMailItem(fetchParams);
    const fetchedData:MailItemResponse = await response.json();
    dispatch(setConfigFlagActionCreator(flags));
    dispatch(setConfigDataActionCreator({ [dataKey]: fetchedData }));
  } catch {
    // To-Do: Handle Errors
    dispatch(setConfigFlagActionCreator(flags));
  }
};
