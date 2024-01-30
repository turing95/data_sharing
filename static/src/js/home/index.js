import { initSmoothScrolling, adjustScrollPosition } from './smoothScrolling.js';
import { initDriveProviderSwitch } from './switchDriveProvider.js';

document.addEventListener('DOMContentLoaded', function() {
        initSmoothScrolling();
        adjustScrollPosition()
        initDriveProviderSwitch() 
});