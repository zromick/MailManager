import { useDispatch, useSelector } from "react-redux";
import { flagsState, FlagsType, getAllMailItemsDataState, GetAllMailItemsDataType } from "../Services/defaults/stateDefaults";
import { GridValueGetter, GridRenderCellParams, GridRowParams, GridPaginationModel } from '@mui/x-data-grid';
import { ConfigFlags, FetchGetAllMailItemsParams, FetchPatchMailItemsParams, MailItem, MailItemPatchData } from "../Services/models/configModels";
import Table from "../Components/Table";
import { Typography } from "@mui/material";
import { DEFAULT_GET_ALL_MAIL_ITEMS_PARAMS, DEFAULT_GET_ALL_MAIL_ITEMS_RESPONSE, DEFAULT_PATCH_MAIL_ITEM_PARAMS } from "../Services/defaults/configDefaults";
import Cell from "../Components/Cell";
import { fetchGetAllMailItemsActionCreator, fetchPatchMailItemActionCreator } from "../Store/actions/configActions";
import { AppDispatch } from "../Store/Store";

const TriageDashboardTable = function RenderTriageDashboardTable() {
const dispatch:AppDispatch = useDispatch();

const allMailItems:GetAllMailItemsDataType = useSelector(getAllMailItemsDataState);
const rows = allMailItems?.items || [];
const limit = allMailItems?.limit ?? DEFAULT_GET_ALL_MAIL_ITEMS_RESPONSE.limit;
const offset = allMailItems?.offset ?? DEFAULT_GET_ALL_MAIL_ITEMS_RESPONSE.offset;
const total = allMailItems?.total ?? DEFAULT_GET_ALL_MAIL_ITEMS_RESPONSE.total;

const flags:FlagsType = useSelector(flagsState);
const isFetchingAllMailItems = (flags & ConfigFlags.FETCH_GET_ALL_MAIL_ITEMS) > 0;

const columnFormat = [
  {
    field: 'mail_item_uuid', description: '', headerText: 'Mail Item UUID', minWidth: 300, valueGetter: undefined, sortable: false
  },
  {
    field: 'mail_item_created_by', description: '', headerText: 'Created By', minWidth: 200, valueGetter: undefined, sortable: false,
  },
  {
    field: 'mail_item_created_time',
    description: '',
    headerText: 'Created Datetime',
    minWidth: 250,
    valueGetter: ((params) => new Date(params)
      .toLocaleString('en-US', { timeZone: 'UTC', timeZoneName: 'short' })) as GridValueGetter,
    sortable: false,
  },
  {
    field: 'mail_item_review_status', description: '', headerText: 'Review Status', minWidth: 150, valueGetter: undefined, sortable: false,
  },
  {
    field: 'mail_item_final_notification_sent',
    description: '',
    headerText: 'Final Notification Sent',
    minWidth: 200,
    valueGetter: (params: boolean) => (params ? 'Yes' : 'No'),
    sortable: false,
  },
];

const columnVisibilityModel = {
  mail_item_uuid: false,
};

const columns = columnFormat.map(((column) => {
  const columnFormatted = {
    field: column.field,
    headerClassName: 'table-column-header',
    description: column.description,
    minWidth: column.minWidth,
    renderHeader: () => <Typography variant="subtitle2">{column.headerText}</Typography>,
    renderCell: (params:GridRenderCellParams) => <Cell params={params} />,
    valueGetter: column.valueGetter,
    sortable: false,
    filterable: false,
  };
  return columnFormatted;
}));

const onRowClick = (params: GridRowParams<MailItem>) => {
  const mailItemPatchData: MailItemPatchData = { ...DEFAULT_PATCH_MAIL_ITEM_PARAMS.mailItemPatchData };
  const fetchPatchMailItemParams: FetchPatchMailItemsParams = {
    mailItemId: params.row.mail_item_uuid,
    mailItemPatchData: mailItemPatchData,
  };
  dispatch(fetchPatchMailItemActionCreator(fetchPatchMailItemParams));
  console.log(`TriageDashboardTable: Dispatched patch for mail item ${params.row.mail_item_uuid} to set status to COMPLETE.`);
};

const handlePaginationModelChange = (model: GridPaginationModel) => {
  if (!isFetchingAllMailItems) {
    const newPage = model.page;
    const newPageSize = model.pageSize;

    const fetchGetAllMailItemsParams: FetchGetAllMailItemsParams = { ...DEFAULT_GET_ALL_MAIL_ITEMS_PARAMS };
    fetchGetAllMailItemsParams.offset = newPage * newPageSize;
    fetchGetAllMailItemsParams.limit = newPageSize;

    dispatch(fetchGetAllMailItemsActionCreator(fetchGetAllMailItemsParams));
    console.log(`TriageDashboardTable: Pagination changed to page ${newPage} (offset ${fetchGetAllMailItemsParams.offset}), page size ${newPageSize}`);
  }
};

return (
  (
    <Table
      columns={columns}
      columnVisibilityModel={columnVisibilityModel}
      hideFooterPagination={false}
      loading={isFetchingAllMailItems}
      onCellClick={() => {}}
      onPaginationModelChange={handlePaginationModelChange}
      onRowClick={onRowClick}
      page={Math.floor(offset / limit)}
      pageSize={limit}
      rowCount={total}
      rows={rows}
    />
  )
);
};

export default TriageDashboardTable;
