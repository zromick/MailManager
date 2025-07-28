// redux reducer state

export const enum ConfigFlags {
  NONE = 0,
  FETCH_GET_MAIL_ITEMS = 1,
  FETCH_GET_ALL_MAIL_ITEMS = 2,
  FETCH_POST_MAIL_ITEMS = 4,
  FETCH_PATCH_MAIL_ITEMS = 8,
}

export const enum ConfigDataKeys {
  FETCH_GET_MAIL_ITEMS = 'fetchGetMailItems',
  FETCH_GET_ALL_MAIL_ITEMS = 'fetchGetAllMailItems',
  FETCH_POST_MAIL_ITEMS = 'fetchPostMailItems',
  FETCH_PATCH_MAIL_ITEMS = 'fetchPatchMailItems',
}

export interface ConfigState {
  api: {
    flags: ConfigFlags,
    data: {
      [ConfigDataKeys.FETCH_GET_MAIL_ITEMS]: MailItemResponse,
      [ConfigDataKeys.FETCH_GET_ALL_MAIL_ITEMS]: GetAllMailItemsResponse,
      [ConfigDataKeys.FETCH_POST_MAIL_ITEMS]: MailItemResponse,
      [ConfigDataKeys.FETCH_PATCH_MAIL_ITEMS]: MailItemResponse,
    },
  },
}

// redux actions

export interface Data {
  [key: string]: any;
}

export enum ConfigActionOptions {
  SET_CONFIG_API_FLAG = 'SET_CONFIG_API_FLAG',
  SET_CONFIG_API_DATA = 'SET_CONFIG_API_DATA',
}

export interface ConfigDataAction {
  type: ConfigActionOptions.SET_CONFIG_API_DATA,
  payload: Data
}

export interface ConfigFlagAction {
  type: ConfigActionOptions.SET_CONFIG_API_FLAG,
  payload: ConfigFlags
}

export type ConfigAction = ConfigDataAction | ConfigFlagAction;

// fetch parameters

export interface FetchGetMailItemsParams {
  mailItemId: string;
}

export interface FetchGetAllMailItemsParams {
  limit: number;
  offset: number;
  ignore_complete: boolean;
  ignore_pending: boolean;
}

export interface FetchPostMailItemsParams {
  mailItemPostData: MailItemPostData;
}

// see: backend/app_common/schemas.py
export interface MailItemPostData {
  mail_item_created_by: string | null
}

export interface FetchPatchMailItemsParams {
  mailItemId: string;
  mailItemPatchData: MailItemPatchData;
}

// see: backend/app_common/schemas.py
export interface MailItemPatchData {
  mail_item_review_status: MailItemStatus | null
  mail_item_final_notification_sent: boolean | null
}


// mail items

export interface GetAllMailItemsResponse {
	items: [MailItem] | [];
	total: number;
  limit: number;
  offset: number;
}

export interface MailItem {
  mail_item_review_status: MailItemStatus;
  mail_item_final_notification_sent: boolean;
  mail_item_created_by: string;
  mail_item_uuid: string;
  mail_item_created_time: string;
}

export interface MailItemResponse extends MailItem {}

export enum MailItemStatus {
  PENDING = 'PENDING',
  COMPLETE = 'COMPLETE',
}
