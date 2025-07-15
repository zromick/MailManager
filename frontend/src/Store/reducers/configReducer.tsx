import { ConfigState, ConfigAction, ConfigActionOptions, ConfigFlags, ConfigDataKeys } from '../../Services/models/configModels';
import { DEFAULT_GET_ALL_MAIL_ITEMS_RESPONSE, DEFAULT_MAIL_ITEMS_RESPONSE } from '../../Services/defaults/configDefaults';

export const ConfigDefaultState: ConfigState = {
  api: {
    flags: ConfigFlags.NONE,
    data: {
      [ConfigDataKeys.FETCH_GET_MAIL_ITEMS]: {...DEFAULT_MAIL_ITEMS_RESPONSE},
      [ConfigDataKeys.FETCH_GET_ALL_MAIL_ITEMS]: {...DEFAULT_GET_ALL_MAIL_ITEMS_RESPONSE},
      [ConfigDataKeys.FETCH_POST_MAIL_ITEMS]: {...DEFAULT_MAIL_ITEMS_RESPONSE},
      [ConfigDataKeys.FETCH_PATCH_MAIL_ITEMS]: {...DEFAULT_MAIL_ITEMS_RESPONSE},
    },
  },
};

function ConfigReducer(
  state:ConfigState = ConfigDefaultState,
  action:ConfigAction,
): ConfigState {
  switch (action.type) {
    case ConfigActionOptions.SET_CONFIG_API_FLAG:
      return {
        ...state,
        api: {
          ...state.api,
          flags: state.api.flags ^ action.payload,
        },
      };
    case ConfigActionOptions.SET_CONFIG_API_DATA:
      return {
        ...state,
        api: {
          ...state.api,
          data: {
            ...state.api.data,
            ...action.payload,
          },
        },
      };
    default:
      return state;
  }
}

export default ConfigReducer;
