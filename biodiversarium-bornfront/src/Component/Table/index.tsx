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
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
        <TableHead>
          <TableRow>
            <TableCell>Nom scientifique</TableCell>
            <TableCell align="right">Nom</TableCell>
            <TableCell align="right">Famille</TableCell>
            <TableCell align="right">Description</TableCell>
            <TableCell align="right">Type</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {fishResult.map((result, index) => (
            <TableRow
              key={index}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">nom_scientifique</TableCell>
              <TableCell align="right">{result.detection}</TableCell>
              <TableCell align="right">family</TableCell>
              <TableCell align="right">description</TableCell>
              <TableCell align="right">s_type</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default ResultTable;