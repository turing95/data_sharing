import { configData } from '../data.js';

let currentDestinationInput = null;
let currentDestinationDisplayInput = null;
let currentAccessTokenInput = null;
let tokenClient;
let accessToken = null;
let refreshToken = null;
let responseGoogle = null;
let pickerInited = false;
let gisInited = false;
function loadScript(url, callback) {
    const script = document.createElement('script');
    script.src = url;
    script.onload = callback;
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);
}

// Export an init function to load external scripts
export function initGooglePicker() {
    loadScript('https://apis.google.com/js/api.js', gapiLoaded);
    loadScript('https://accounts.google.com/gsi/client', gisLoaded);
    // ... [any other initialization code]
}

//document.getElementById('authorize_button').style.visibility = 'hidden';
document.getElementById('signout_button').style.visibility = 'hidden';

/**
* Callback after api.js is loaded.
*/
function gapiLoaded() {
gapi.load('client:picker', initializePicker);
}

/**
* Callback after the API client is loaded. Loads the
* discovery doc to initialize the API.
*/
async function initializePicker() {
await gapi.client.load('https://www.googleapis.com/discovery/v1/apis/drive/v3/rest');
pickerInited = true;
maybeEnableButtons();
}

/**
* Callback after Google Identity Services are loaded.
*/
function gisLoaded() {
tokenClient = google.accounts.oauth2.initTokenClient({
    client_id: configData.googleClientId,
    scope: configData.googleScopes.join(' '),
    access_type: 'offline', // Request a refresh token.
    prompt: 'consent',      // Force the consent prompt to ensure a refresh token is returned.
    callback: '', // defined later
});
gisInited = true;
maybeEnableButtons();
}

/**
* Enables user interaction after all libraries are loaded.
*/
function maybeEnableButtons() {
if (pickerInited && gisInited) {
  //document.getElementById('authorize_button').style.visibility = 'visible';
}
}

/**
*  Sign in the user upon button click.
*/
export function handleAuthClick(buttonElement) {
const parentDiv = buttonElement.closest('.mb-6');

// Find the input within this div
// Store the reference to this specific destinationInput
const regexDestination = /^id_requests-\d+-destination$/;
const regexDestinationDisplay = /^id_requests-\d+-destination_display$/;
const regexToken = /^id_requests-\d+-token$/;
currentDestinationInput = Array.from(parentDiv.querySelectorAll('input')).find(input => regexDestination.test(input.id));
currentDestinationDisplayInput = Array.from(parentDiv.querySelectorAll('input')).find(input => regexDestinationDisplay.test(input.id));
currentAccessTokenInput = Array.from(parentDiv.querySelectorAll('input')).find(input => regexToken.test(input.id));

tokenClient.callback = async (response) => {
  if (response.error !== undefined) {
    throw (response);
  }
  refreshToken = response.refresh_token;
  accessToken = response.access_token;
  responseGoogle = response
  document.getElementById('signout_button').style.visibility = 'visible';
  await createPicker();
};
if (!accessToken) {
  tokenClient.requestAccessToken({prompt: 'consent'});

} else {
// If the token is available, use it and proceed to create the picker
document.getElementById('signout_button').style.visibility = 'visible';
createPicker();
}


}

/**
*  Sign out the user upon button click.
*/
export function handleSignoutClick() {
if (accessToken) {
  accessToken = null;
  google.accounts.oauth2.revoke(accessToken);
  document.getElementById('signout_button').style.visibility = 'hidden';
}
}

/**
*  Create and render a Picker object for searching images.
*/
function createPicker() {
  const picker = new google.picker.PickerBuilder()
    .enableFeature(google.picker.Feature.NAV_HIDDEN)
    .enableFeature(google.picker.Feature.MULTISELECT_ENABLED)
    .setDeveloperKey(configData.googleApiKey)
    .setAppId(configData.googleAppId)
    .setOAuthToken(accessToken)
    .addView(new google.picker.DocsView(google.picker.ViewId.FOLDERS)
        .setSelectFolderEnabled(true))
    .setCallback(pickerCallback)
    .build();
picker.setVisible(true);
}

/**
* Displays the file details of the user's selection.
* @param {object} data - Containers the user selection from the picker
*/
async function pickerCallback(data) {
if (data.action === google.picker.Action.PICKED) {
    let text = `Picker response: \n${JSON.stringify(data, null, 2)}\n`;
    // Assuming the first selected item is a folder
    const folder = data[google.picker.Response.DOCUMENTS][0];
    const folderId = folder[google.picker.Document.ID];
    const folderName = folder[google.picker.Document.NAME];  // Get the folder name

    // Use the stored input element
    if (currentDestinationInput) {
        currentDestinationInput.value = folderId;
        currentDestinationDisplayInput.value = folderName;
        currentAccessTokenInput.value = accessToken;
    }
}
}