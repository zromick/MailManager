import {
DataGrid, GridColDef, GridCellParams, GridRowParams, GridPaginationModel,
} from '@mui/x-data-grid';
import { Box } from '@mui/material';

export interface TableProps {
columns: GridColDef[],
columnVisibilityModel: { [key:string]: boolean } | undefined,
hideFooterPagination: boolean,
loading:boolean,
onCellClick: (params:GridCellParams) => void,
onPaginationModelChange: (model: GridPaginationModel) => void,
onRowClick?: (params:GridRowParams) => void,
page:number,
pageSize:number,
rowCount:number,
rows: any[],
id?: string,
}

const Table = function RenderTable(props:TableProps) {
const {
  columns,
  columnVisibilityModel,
  hideFooterPagination,
  loading,
  onCellClick,
  onPaginationModelChange,
  onRowClick,
  page,
  pageSize,
  rowCount,
  rows,
  id,
} = props;

const rowsWithId = rows.map((row: any) => ({
  ...row,
  id: row.mail_item_uuid,
}));

return (
  <Box
    id={id}
    sx={{
      height: '100%',
      width: '100%',
    }}
  >
    <DataGrid
      columns={columns}
      columnVisibilityModel={columnVisibilityModel}
      disableColumnSelector
      hideFooterPagination={hideFooterPagination}
      loading={loading}
      onCellClick={onCellClick}
      onPaginationModelChange={onPaginationModelChange}
      onRowClick={onRowClick}
      pageSizeOptions={[10, 15]}
      paginationModel={{ page, pageSize }}
      pagination
      paginationMode="server"
      rowCount={rowCount}
      rowHeight={40}
      rows={loading ? [] : rowsWithId}
      slotProps={{
        loadingOverlay: {
          variant: 'linear-progress',
          noRowsVariant: 'skeleton',
        },
      }}
      sx={{
        border: 1,
        borderColor: 'grey.400',
        bgcolor: 'background.paper',
        '& .MuiDataGrid-toolbarContainer': {
          borderBottom: 'solid 1px',
          borderColor: 'grey.300',
        },
      }}
    />
  </Box>
);
};

export default Table;
