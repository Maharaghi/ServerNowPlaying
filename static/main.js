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

    function fetchData() {
        window.fetch(`/api/status/${id}`).then(r => r.json()).then(data => {
            if (!data || data === 'None') return;
            if (shallowEqual(data, lastData)) return;

            console.log(data);

            updateIfNotEqual(state, 'State: ' + data.state);
            updateIfNotEqual(track, 'Track: ' + data.track);
            updateIfNotEqual(artist, 'Artist: ' + data.artist);

            if (data.album) {
                updateIfNotEqual(album, 'Album: ' + data.album);
                album.hidden = false;
            } else album.hidden = true;

            if (data.image && thumbnail.src !== data.image) {
                thumbnail.src = data.image;
                thumbnail.hidden = false;
            } else if (lastData.track !== data.track) 
                thumbnail.hidden = true;

            lastData = data;
        }).catch((e) => {
            console.error(e);
            // Assume we failed to parse JSON data, and thus no info exist
            updateIfNotEqual(state, 'No data :(');
            updateIfNotEqual(track, 'Try playing something');
            updateIfNotEqual(artist, '');
            updateIfNotEqual(album, '');
            thumbnail.hidden = true;
        });
    }

    setInterval(fetchData, 2500);
    fetchData();
})();