# FeedCare AI API integration sketch

## Frontend replacement
Replace the mock functions in `index.html`:

```js
async function analyzeFeed(payload) {
  const response = await fetch('/api/analyze-feed/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(payload)
  });
  if (!response.ok) throw new Error('Analysis failed');
  return await response.json();
}
```

The same pattern can be used for `/api/analyze-silage/`.

## Production note
The server should authenticate the farmer, validate image MIME/type and size, authorize access to test records, run the ML model, store the result, and return a versioned analysis response.
