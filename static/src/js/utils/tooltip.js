export function initTooltip(labelElement) {
    let element = labelElement.querySelector('[role="tooltip"]');
    let button = labelElement.querySelector('button');
    if (!element || !button) {
        return;
    }
    let tooltip = new Tooltip(element, button);
}