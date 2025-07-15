import MainLayout from '../MainLayout/MainLayout';
import { useRoutes } from 'react-router-dom';
import TriageDashboard from '../TraigeDashboard/TriageDashboard';

const routes = {
  path: '/',
  element: <MainLayout />,
  children: [
    {
      path: '/',
      element: <TriageDashboard />,
    },
  ],
};


export default function Router() {
  return useRoutes([routes]);
}
