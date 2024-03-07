import { initSocialAccountsTable } from './socialAccounts.js';
import {initTooltip} from "../../utils/tooltip.js";

document.addEventListener('DOMContentLoaded', function() {
    initSocialAccountsTable();
});

document.body.addEventListener('htmx:afterSettle', function(evt) {
    evt.target.querySelectorAll('label').forEach(initTooltip);
});