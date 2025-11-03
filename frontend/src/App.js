import React from "react";
import { Container, AppBar, Tabs, Tab, Box } from "@mui/material";
import BrainTumorPage from "./components/BrainTumorPage";
import GeneralAnalysisPage from "./components/GeneralAnalysisPage";

function App() {
  const [tab, setTab] = React.useState(0);
  const handleTabChange = (e, newValue) => setTab(newValue);

  return (
    <Container>
      <AppBar position="static" color="default">
        <Tabs value={tab} onChange={handleTabChange} centered>
          <Tab label="Brain Tumor Detection" />
          <Tab label="General Image Analysis" />
        </Tabs>
      </AppBar>
      <Box mt={4}>
        {tab === 0 ? <BrainTumorPage /> : <GeneralAnalysisPage />}
      </Box>
    </Container>
  );
}

export default App;
