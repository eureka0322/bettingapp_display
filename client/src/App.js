import * as React from 'react';
import axios from 'axios';
import {Card, CardHeader, CardContent, Typography, Box} from '@mui/material'
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

export default function App() {
  const [betevoList, setBetevoList] = React.useState([]);

  const getAllList = async () => {
    try {
      await axios
        .get('/api')
        .then((response) => {
          setBetevoList(response.data);
        });
    } catch (err) {
      console.error(err.message);
    }
  };

  React.useEffect(() => {
    getAllList();
  }, []);

  return (
    <Box width={1200} sx={{ margin: '32px'}}>
      {
        betevoList.map((betevo)=> (
          <Card key={betevo.game_id+betevo.category} sx={{border: '1px solid #3b82f6', marginTop: 2}}>
            <CardHeader
              title={betevo.game_title+' | '+betevo.category}
              sx={{
                background: '#3b82f6',
                color: 'white'
              }}
            >
            
            </CardHeader>
            <CardContent>
              <Table sx={{minWidth: 650}} aria-label='betting app table'>
                <TableHead>
                  <TableRow>
                    <TableCell>Team</TableCell>
                    <TableCell>Spread_ODD</TableCell>
                    <TableCell>Spread_Standard</TableCell>
                    <TableCell>Money_Line</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {
                    betevo.details.map((teamData)=>(
                      <TableRow key={teamData.id}>
                        <TableCell>{teamData.team_name}</TableCell>
                        <TableCell>{teamData.spread_odd}</TableCell>
                        <TableCell>{teamData.spread_standard}</TableCell>
                        <TableCell>{teamData.money_line}</TableCell>
                      </TableRow>
                    ))
                  }
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        ))
      }
    </Box>
  );
}
