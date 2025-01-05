import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import ResultPage from "./ResultPage";
import AnalyzePage from "./AnalyzePage";
import GeneratePage from "./GeneratePage";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/analyze" element={<AnalyzePage />} />
        <Route path="/generate" element={<GeneratePage />} />
        <Route path="/result" element={<ResultPage />} />
      </Routes>
    </Router>
  </React.StrictMode>
);

reportWebVitals();
