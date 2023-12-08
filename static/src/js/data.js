/**
* @typedef {Object} ConfigData
* @property {string} googleApiKey - The API key for the application.
* @property {string} googleClientId - The client ID for the OAuth provider.
* @property {string} googleAppId - The application ID.
* @property {string[]} googleScopes - The authorization scopes required by the API.
*/
/**
* @type {ConfigData}
*/
export const configData = JSON.parse(document.getElementById('config-data').textContent);
configData.googleScopes = ['https://www.googleapis.com/auth/drive'];
