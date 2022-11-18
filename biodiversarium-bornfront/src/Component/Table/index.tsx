import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

interface ResultTableProps {
  fishResult: {
    certainty: number,
    detection: string,
    position: { 
            bottomright: { x: number, y: number },
            topleft: { x: number, y: number }
    }
  }[];
}

const ResultTable: React.FC<ResultTableProps> = (Props) => {
  const { fishResult } = Props;
  return (
    <TableContainer style={{height: '50%'}} component={Paper}>
      <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
        <TableHead>
          <TableRow>
            {/*<TableCell>Nom scientifique</TableCell>*/}
            <TableCell align="left">Nom</TableCell>
            {/*<TableCell align="right">Famille</TableCell>*/}
            <TableCell align="left">Description</TableCell>
            {/*<TableCell align="right">Type</TableCell>*/}
            <TableCell align="left">Précision IA (%)</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {fishResult.map((result, index) => 
          result.certainty > 0.5 ?
          (<TableRow
              key={index}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              {/*<TableCell component="th" scope="row">nom_scientifique</TableCell>*/}
              <TableCell align="left">{result.detection}</TableCell>
              {/*<TableCell align="right">family</TableCell>*/}
              <TableCell align="left">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum</TableCell>
              {/*<TableCell align="right">s_type</TableCell>*/}
              <TableCell align="left">{(result.certainty*100).toFixed(2)}%</TableCell>
            </TableRow>
          ) : '')}
          {!fishResult.length ? 'Impossible d\'identifier ce spécimen' : ''}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default ResultTable;