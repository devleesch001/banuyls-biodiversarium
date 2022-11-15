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
            id: number,
            scientific_name: string,
            name: string,
            family: string,
            description: { fr: string },
            s_type: string,
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
          {fishResult.map((result) => (
            <TableRow
              key={result.id}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">{result.name}</TableCell>
              <TableCell align="right">{result.family}</TableCell>
              <TableCell align="right">{result.description.fr}</TableCell>
              <TableCell align="right">{result.s_type}</TableCell>
              <TableCell align="right">{result.s_type}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default ResultTable;