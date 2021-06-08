/**
 * This partial file uses the same amount of data as the full one, since it receives the full object anyway.
 * Might fix this in the future to only send the target data, but it's such a small amount that it really shouldn't matter.
 */
// Do not pollute global scope
(() => {
    const re = /^(?:\/status\/)(\w+)\/(\w+)/gm;
    const testId = re.exec(window.location.pathname);
    const [, userID, initTarget] = testId;

    const target = initTarget === 'thumbnail' ? 'image' : initTarget;

    // Might wanna change this to something other than alert... maybe
    if (!userID || !target) return alert('Invalid URL');

    // Create references to the elements that we update
    const dataElement = document.querySelector('#data');
    const thumbnailElement = document.querySelector('#thumb');

    let lastData = null;

    function updateIfNotEqual(element, data) {
        if (element.textContent !== data) {
            // Make sure elements are properly shown I guess
            dataElement.hidden = false;
            thumbnailElement.hidden = true;
            element.textContent = data;
        }
    }

    function quickhash(str) {
        let hash = 0, i, chr;
        if (str.length === 0) return hash;
        for (i = 0; i < str.length; i++) {
            chr = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + chr;
            hash |= 0; // Convert to 32bit integer
        }
        return hash;
    };

    // Just check shallow equality, we probably don't need deep checks (yet?)
    function shallowEqual(object1, object2) {
        // If we have a null object on any instance we return
        if ((!object1 && object2) || (object1 && !object2)) return false;
        else if (object1 === object2) return true;

        const keys1 = Object.keys(object1);
        const keys2 = Object.keys(object2);

        if (keys1.length !== keys2.length) return false;

        for (let key of keys1)
            if (object1[key] !== object2[key]) return false;


        return true;
    }

    function setData(data) {
        if (target === 'image') setThumbnail(data);
        else if (data[target]) updateIfNotEqual(dataElement, data[target]);
        else if (target === 'album') updateIfNotEqual(dataElement, '');
        else updateIfNotEqual(dataElement, 'Invalid path. Try any of [ artist, track, album, state, image|thumbnail ]');
        lastData = data;
    }

    function setThumbnail(data) {
        dataElement.hidden = true;
        const album = (data.album) ? data.album : '';
        const imsrc = data.image ? `${data.image}?id=${quickhash(data.track + data.artist + album)}` : '';

        if (data.image && thumbnail.src !== imsrc) {
            thumbnailElement.src = imsrc;
            thumbnailElement.hidden = false;
        } else if (lastData.track !== data.track && !data.image)
            thumbnailElement.hidden = true;
    }

    function setNoData() {
        updateIfNotEqual(dataElement, 'No data :(');
    }

    const socket = io();
    socket.on('connect', () => {
        socket.emit('status', userID);
        socket.emit('join', userID);
    });

    socket.on('join', console.log);
    socket.on('status', (data) => {
        if (!data || data === 'None') return setNoData();
        if (shallowEqual(data, lastData)) return;
        setData(data);
    });
})();
