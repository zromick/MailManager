import { FetchGetAllMailItemsParams, FetchPatchMailItemsParams, GetAllMailItemsResponse, MailItemResponse, MailItemStatus } from '../models/configModels';


export const DEFAULT_MAIL_ITEMS_RESPONSE:MailItemResponse = {
mail_item_review_status: MailItemStatus.PENDING,
mail_item_final_notification_sent: false,
mail_item_created_by: '',
mail_item_uuid: '',
mail_item_created_time: new Date().toISOString(),
};

export const DEFAULT_GET_ALL_MAIL_ITEMS_PARAMS:FetchGetAllMailItemsParams = {
	"limit": 10,
	"offset": 0,
	"ignore_complete": false,
	"ignore_pending": false,
}

export const DEFAULT_GET_ALL_MAIL_ITEMS_RESPONSE:GetAllMailItemsResponse = {
	"items": [],
	"total": 0,
	"limit": 10,
	"offset": 0,
};

export const DEFAULT_PATCH_MAIL_ITEM_PARAMS:FetchPatchMailItemsParams = {
	mailItemId: '', // Will be overridden when used
	mailItemPatchData: {
		mail_item_review_status: MailItemStatus.COMPLETE,
		mail_item_final_notification_sent: false,
	}
};

export const DEFAULT_MAIL_ITEMS_PAGINATION = {
  page: 0,
  limit: 10,
};

export const DEFAULT_SENDER_EMAIL = "zac.romick@gmail.com";
