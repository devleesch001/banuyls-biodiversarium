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
    s_name: string,
    s_type: string,
    family: string,
    description: string,
    position: { 
            bottomright: { x: number, y: number },
            topleft: { x: number, y: number }
    }
  }[];
}

const ResultTable: React.FC<ResultTableProps> = (Props) => {
  const { fishResult } = Props;
  return (
    <TableContainer style={{height: '100%'}} component={Paper}>
      <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
        <TableHead>
          <TableRow>
            <TableCell align="left">Nom</TableCell>
            <TableCell>Nom scientifique</TableCell>
            <TableCell align="right">Famille</TableCell>
            <TableCell align="right">Type</TableCell>
            <TableCell align="left">Description</TableCell>
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
              <TableCell component="th" scope="row" align="left">{result.detection}</TableCell>
              <TableCell align="left">{result.s_name}</TableCell>
              <TableCell align="left">{result.family}</TableCell>
              <TableCell align="left">{result.s_type}</TableCell>
              <TableCell align="left">{result.description}</TableCell>
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