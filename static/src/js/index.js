import {initMessageBar} from "./utils/messageBar.js";
import { initSubmitButtons } from './utils/submitButton.js';
import { initSmoothScrolling, adjustScrollPositionOnPageLoad } from './utils/smoothScrolling.js';
import { initNav } from './utils/navbar.js';

document.addEventListener('DOMContentLoaded', function() {
        initSubmitButtons();
        initMessageBar();
        initSmoothScrolling();
        adjustScrollPositionOnPageLoad()
        initNav();
});

