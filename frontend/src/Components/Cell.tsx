import { Tooltip, Typography } from '@mui/material';
import { GridRenderCellParams } from '@mui/x-data-grid';

export interface CellProps {
  params: GridRenderCellParams
}

function Cell(props:CellProps) {
  const { params } = props;
  const tooltipVisibleMinLength = 15;
  const tooltipVisibleMaxWidth = 225;

  const cellText = (
    <Typography style={{ overflow: 'hidden', textOverflow: 'ellipsis' }}>
      {params.value}
    </Typography>
  );

  return (
    <div>
      {params?.value?.length >= tooltipVisibleMinLength && params.colDef.computedWidth <= tooltipVisibleMaxWidth
        ? (
          <Tooltip
            disableHoverListener={false}
            title={params.value}
          >
            {cellText}
          </Tooltip>
        )
        : cellText}
    </div>

  );
}

export default Cell;
