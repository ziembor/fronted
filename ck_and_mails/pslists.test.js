const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];

function createPage() {
    const elements = new Map();
    const document = {
        getElementById(id) {
            if (!elements.has(id)) {
                elements.set(id, {
                    value: '',
                    innerHTML: '',
                    textContent: '',
                    addEventListener(event, callback) {
                        this[event] = callback;
                    }
                });
            }
            return elements.get(id);
        }
    };
    vm.runInNewContext(script, { document });
    return elements;
}

test('pslists groups distinct extracted values into named PowerShell arrays', () => {
    const elements = createPage();
    elements.get('inputText').value = [
        'AB12CD XY34ZW AB12CD AD\\PQ56RS',
        'first@example.com second@example.com first@example.com',
        'MN78GHLSA mbxteam ML-team NPB2user 192.168.1.1',
        'su800host 12345678-1234-1234-1234-123456789abc'
    ].join(' ');
    elements.get('inputText').input();

    assert.equal(elements.get('pslists').value, [
        '$cks = @("AB12CD", "XY34ZW", "AD\\PQ56RS")',
        '$mails = @("first@example.com", "second@example.com")',
        '$lsas = @("MN78GHLSA")',
        '$mailboxes = @("mbxteam")',
        '$mailingLists = @("ML-team")',
        '$nonPersonalUsers = @("NPB2user")',
        '$ipv4s = @("192.168.1.1")',
        '$hostnames = @("su800host")',
        '$guids = @("12345678-1234-1234-1234-123456789abc")'
    ].join('\n'));
});

test('pslists omits empty categories and clears when input is cleared', () => {
    const elements = createPage();
    elements.get('inputText').value = 'one@example.com';
    elements.get('inputText').input();
    assert.equal(elements.get('pslists').value, '$mails = @("one@example.com")');

    elements.get('inputText').value = '';
    elements.get('inputText').input();
    assert.equal(elements.get('pslists').value, '');
});
