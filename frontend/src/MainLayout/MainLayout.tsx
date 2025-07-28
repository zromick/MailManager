import { Outlet } from 'react-router-dom';
import MailLogoUrl from '../assets/mail-logo.svg';
import { Typography } from '@mui/material';
import { DEFAULT_ALL_MAIL_PAGE_DESCRIPTION, DEFAULT_ALL_MAIL_PAGE_HEADER, DEFAULT_COPYRIGHT } from '../Services/defaults/formDefaults';

import './MainLayout.css';

function MainLayout() {
return (
<div className="app-root-container">
    <div className="main-layout-outer-wrapper">
        <div className="main-layout-outer">
            <div className="main-layout-inner">
                <div className="main-layout-top-content-wrapper">
                    <div className="main-layout-header">
                        <img src={MailLogoUrl} alt="Mailbox Logo" className="main-layout-logo" />
                    </div>

                    <div className="main-layout-content">
                        <Typography
                            variant="h4"
                            sx={{
                                fontFamily: 'SF Pro, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"',
                                fontWeight: 400,
                                fontSize: '36px',
                                lineHeight: '100%',
                                letterSpacing: '0%',
                                color: 'var(--Mail-Blue-500)'
                            }}
                        >
                            {DEFAULT_ALL_MAIL_PAGE_HEADER}
                        </Typography>
                    </div>
                    <div className="main-layout-content">
                        <Typography
                            variant="subtitle1"
                            sx={{
                                fontFamily: 'SF Pro, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"',
                                fontWeight: 400,
                                fontSize: '22px',
                                lineHeight: '100%',
                                letterSpacing: '0%',
                            }}
                        >
                            {DEFAULT_ALL_MAIL_PAGE_DESCRIPTION}
                        </Typography>
                    </div>
                    <div className="main-layout-content">
                        <Outlet />
                    </div>
                </div>

                <footer className="main-layout-footer">
                    <Typography variant="caption" color="text.secondary">
                        {DEFAULT_COPYRIGHT}
                    </Typography>
                </footer>
            </div>
        </div>
    </div>
</div>
);
}

export default MainLayout;
