// General defaults

export const DEFAULT_ALL_MAIL_PAGE_HEADER = "All Mail";
export const DEFAULT_RELOAD_TIME_MS = 20000; // in milliseconds
export const DEFAULT_ALL_MAIL_PAGE_DESCRIPTION = `Below are all of the mail item statuses. Refreshes automatically every ${DEFAULT_RELOAD_TIME_MS/1000} seconds.`;

// Date-related defaults

export const DATE_TODAY:Date = new Date(); // Today
export const DEFAULT_COPYRIGHT:string = `MailManager © ${DATE_TODAY.getFullYear()}`;
