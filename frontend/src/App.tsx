import Router from './Router/Router';
import { BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from './Store/Store';

export const App = () => {
  const baseUrl = "/";
  return (
    <BrowserRouter basename={baseUrl}>
      <Provider store={store}>
        <Router />
      </Provider>
    </BrowserRouter>
  );
};
