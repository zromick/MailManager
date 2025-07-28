
import { host, mailItemsQuery } from '../defaults/apiDefaults';
import { FetchGetAllMailItemsParams, FetchGetMailItemsParams, FetchPatchMailItemsParams, FetchPostMailItemsParams } from '../models/configModels';


export const fetchGetMailItem:((fetchParams: FetchGetMailItemsParams) => Promise<Response>) = (fetchParams) => {
  const { mailItemId } = fetchParams;
  return callServiceAsPromise(`${host}${mailItemsQuery}/${mailItemId}`);
}

export const fetchGetAllMailItems:((fetchParams:FetchGetAllMailItemsParams) => Promise<Response>) = (fetchParams) => {
  const { limit, offset, ignore_complete, ignore_pending } = fetchParams;
  return callServiceAsPromise(`${host}${mailItemsQuery}?limit=${limit}&offset=${offset}&ignore_complete=${ignore_complete}&ignore_pending=${ignore_pending}`);
}

export const fetchPostMailItem:((fetchParams: FetchPostMailItemsParams) => Promise<Response>) = (fetchParams) => {
  const { mailItemPostData } = fetchParams;
  const body = JSON.stringify(mailItemPostData);
  return callServiceAsPromise(`${host}${mailItemsQuery}`, 'POST', body);
};

export const fetchPatchMailItem:((fetchParams: FetchPatchMailItemsParams) => Promise<Response>) = (fetchParams) => {
  const { mailItemId, mailItemPatchData } = fetchParams;
  const body = JSON.stringify(mailItemPatchData);
  return callServiceAsPromise(`${host}${mailItemsQuery}/${mailItemId}`, 'PATCH', body );
};

async function callServiceAsPromise(url = '', method = 'GET', data: BodyInit | string | null = null) {
  return fetch(url, {
    method,
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {'Content-Type': 'application/json'},
    body: data,
    redirect: 'follow',
    referrerPolicy: 'no-referrer-when-downgrade',
  });
}
