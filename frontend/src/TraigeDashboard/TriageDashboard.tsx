import TriageDashboardTable from "./TriageDashboardTable";
import { FetchGetAllMailItemsParams, FetchPostMailItemsParams } from "../Services/models/configModels";
import { fetchGetAllMailItemsActionCreator, fetchPostMailItemActionCreator } from "../Store/actions/configActions";
import { useDispatch } from "react-redux";
import { AppDispatch } from "../Store/Store";
import { useEffect } from "react";
import { DEFAULT_GET_ALL_MAIL_ITEMS_PARAMS, DEFAULT_SENDER_EMAIL } from "../Services/defaults/configDefaults";
import { DEFAULT_RELOAD_TIME_MS } from "../Services/defaults/formDefaults";

const TriageDashboard: React.FC = () => {
const dispatch: AppDispatch = useDispatch();

useEffect(() => {
    const dashboardFetchGetAllMailItems = () => {
      const fetchGetAllMailItemsParams: FetchGetAllMailItemsParams = { ...DEFAULT_GET_ALL_MAIL_ITEMS_PARAMS };
      dispatch(fetchGetAllMailItemsActionCreator(fetchGetAllMailItemsParams));
      // TODO: Refresh with current page params (offset, limit) from Redux state.
      // Requires a second useEffect that tracks initial state (as to not double the call).
    };

    const initialLoadSequence = async () => {
      const fetchPostMailItemParams: FetchPostMailItemsParams = {
        mailItemPostData: {mail_item_created_by: DEFAULT_SENDER_EMAIL},
      };
      // await dispatch(fetchPostMailItemActionCreator(fetchPostMailItemParams)); // Optionally post a new mail item first, then fetch all mail items

      dashboardFetchGetAllMailItems();
    };

    initialLoadSequence();

    const intervalId = setInterval(dashboardFetchGetAllMailItems, DEFAULT_RELOAD_TIME_MS); // Fetch GET All every X seconds

    return () => clearInterval(intervalId);
  }, [dispatch]);

  return (
    <TriageDashboardTable />
  );
};

export default TriageDashboard;
