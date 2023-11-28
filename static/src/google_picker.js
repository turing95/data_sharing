  /* exported gapiLoaded */
  /* exported gisLoaded */
  /* exported handleAuthClick */
  /* exported handleSignoutClick */
/**
 * @typedef {Object} ConfigData
 * @property {string} googleApiKey - The API key for the application.
 * @property {string} googleClientId - The client ID for the OAuth provider.
 * @property {string} googleAppId - The application ID.
 * @property {string[]} googleScopes - The authorization scopes required by the API.
 */
  // Authorization scopes required by the API; multiple scopes can be
  // included, separated by spaces.

  /**
 * @type {ConfigData}
 */
  const config_data = JSON.parse(document.getElementById('config-data').textContent);
  config_data.googleScopes = ['https://www.googleapis.com/auth/drive'];


  let tokenClient;
  let accessToken = null;
  let pickerInited = false;
  let gisInited = false;


  document.getElementById('authorize_button').style.visibility = 'hidden';
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
      client_id: config_data.googleClientId,
      scope: config_data.googleScopes.join(' '),
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
      document.getElementById('authorize_button').style.visibility = 'visible';
    }
  }

  /**
   *  Sign in the user upon button click.
   */
  function handleAuthClick() {


    tokenClient.callback = async (response) => {
      if (response.error !== undefined) {
        throw (response);
      }
      accessToken = response.access_token;
      document.getElementById('signout_button').style.visibility = 'visible';
      document.getElementById('authorize_button').innerText = 'Refresh';
      await createPicker();
    };
    if (!accessToken) {
      tokenClient.requestAccessToken({prompt: 'consent'});

  } else {
    // If the token is available, use it and proceed to create the picker
    document.getElementById('signout_button').style.visibility = 'visible';
    document.getElementById('authorize_button').innerText = 'Refresh';
    createPicker();
  }


  }

  /**
   *  Sign out the user upon button click.
   */
  function handleSignoutClick() {
    if (accessToken) {
      accessToken = null;
      google.accounts.oauth2.revoke(accessToken);
      document.getElementById('content').innerText = '';
      document.getElementById('authorize_button').innerText = 'Authorize';
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
        .setDeveloperKey(config_data.googleApiKey)
        .setAppId(config_data.googleAppId)
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
        console.log(folderId);

        // Fetch details about the folder
        const res = await gapi.client.drive.files.get({
            'fileId': folderId,
            'fields': '*',
            'supportsAllDrives': true
        });

        text += `Drive API response for selected folder: \n${JSON.stringify(res.result, null, 2)}\n`;
        window.document.getElementById('content').innerText = text;
    }
}