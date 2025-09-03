import { createBrowserRouter } from "react-router-dom";
import Layout from "../layout/Layout.jsx";
import Home from "../pages/Home.jsx";
import LinkAnalysis from "../pages/LinkAnalysis.jsx";
import Reports from "../pages/Reports.jsx";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: "link-analysis", element: <LinkAnalysis /> },
      { path: "reports", element: <Reports /> },
      { path: "*", element: <div>Not Found</div> }
    ]
  }
]);