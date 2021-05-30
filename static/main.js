// Do not pollute global scope
(() => {
    // Slice the pathname to get the id that we use to update
    const id = window.location.pathname.slice(window.location.pathname.indexOf('/status') + '/status'.length + 1);

    // This could be used to create filters such as show,hide etc.
    const filters = new URLSearchParams(window.location.search);

    console.log(id);
    console.log(Array.from(filters.keys()));

    // Create references to the elements that we update
    const state = document.querySelector('#state');
    const track = document.querySelector('#track');
    const artist = document.querySelector('#artist');
    const album = document.querySelector('#album');
    const thumbnail = document.querySelector('#thumbnail');

    let lastData = {};

    function updateIfNotEqual(element, data) {
        if (element.textContent !== data)
            element.textContent = data;
    }

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

    // function fetchData() {
    //     window.fetch(`/api/status/${id}`).then(r => r.json()).then(data => {
    //         if (!data || data === 'None') return;
    //         if (shallowEqual(data, lastData)) return;

    //         console.log(data);

    //         updateIfNotEqual(state, 'State: ' + data.state);
    //         updateIfNotEqual(track, 'Track: ' + data.track);
    //         updateIfNotEqual(artist, 'Artist: ' + data.artist);

    //         if (data.album) {
    //             updateIfNotEqual(album, 'Album: ' + data.album);
    //             album.hidden = false;
    //         } else album.hidden = true;

    //         if (data.image && thumbnail.src !== data.image) {
    //             thumbnail.src = data.image;
    //             thumbnail.hidden = false;
    //         } else if (lastData.track !== data.track && !data.image)
    //             thumbnail.hidden = true;

    //         lastData = data;
    //     }).catch((e) => {
    //         console.error(e);
    //         // Assume we failed to parse JSON data, and thus no info exist
    //         updateIfNotEqual(state, 'No data :(');
    //         updateIfNotEqual(track, 'Try playing something');
    //         updateIfNotEqual(artist, '');
    //         updateIfNotEqual(album, '');
    //         thumbnail.hidden = true;
    //     });
    // }

    function quickhash(str) {
        var hash = 0, i, chr;
        if (str.length === 0) return hash;
        for (i = 0; i < str.length; i++) {
            chr = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + chr;
            hash |= 0; // Convert to 32bit integer
        }
        return hash;
    };

    function setData(data) {
        console.log(data);

        if(!filters.has('select')){
            updateIfNotEqual(state, 'State: ' + data.state);
            updateIfNotEqual(track, 'Track: ' + data.track);
            updateIfNotEqual(artist, 'Artist: ' + data.artist);

            if (data.album) {
                updateIfNotEqual(album, 'Album: ' + data.album);
                album.hidden = false;
            } else album.hidden = true;

            setThumbnail(data);
        }
        else {
            var selector = filters.get('select');
            state.hidden     = selector === 'state';
            track.hidden     = selector === 'track';
            artist.hidden    = selector === 'artist';
            album.hidden     = selector === 'album';
            thumbnail.hidden = selector === 'thumbnail';

            switch(selector) {
                case 'state':
                    updateIfNotEqual(state, data.state);
                    break;
                case 'track':
                    updateIfNotEqual(track, data.track);
                    break;
                case 'artist':
                    updateIfNotEqual(artist, data.artist);
                    break;
                case 'album':
                    if (data.album) {
                        updateIfNotEqual(album, data.album);
                        album.hidden = false;
                    } else album.hidden = true;
                    break;
                case 'thumbnail':
                    setThumbnail(data);
                    break;
            }
        }

        lastData = data;
    }

    function setThumbnail(data) {
        const imsrc = data.image ? `${data.image}?id=${quickhash(data.track + data.artist)}` : '';

        if (data.image && thumbnail.src !== imsrc) {
            thumbnail.src = imsrc;
            thumbnail.hidden = false;
        } else if (lastData.track !== data.track && !data.image)
            thumbnail.hidden = true;
    }

    function setNoData() {
        updateIfNotEqual(state, 'No data :(');
        updateIfNotEqual(track, 'Try playing something');
        updateIfNotEqual(artist, '');
        updateIfNotEqual(album, '');
        thumbnail.hidden = true;
    }

    // setInterval(fetchData, 2500);
    // fetchData();
    const socket = io();
    socket.on('connect', () => {
        socket.emit('status', id);
        socket.emit('join', id);
    });

    socket.on('join', console.log);
    socket.on('status', (data) => {
        if (!data || data === 'None') return setNoData();
        if (shallowEqual(data, lastData)) return;
        setData(data);
    });
})();
