import {render, html} from './preact.mjs';
import {App} from './components/app.mjs'

render(html`<${App} />`, document.body);