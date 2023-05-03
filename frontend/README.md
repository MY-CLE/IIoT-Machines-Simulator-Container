### Start the development Process

To start the frontend development we first need to start the react development server.

1.

```
npm run start
```
2.

In a second termial we need to activate tailwind watch to update the input.css while development.


```
npx tailwindcss -i ./input.css -o ./src/css/output.css --watch
```

In VSCode you can activate the watch to automatically recompile all .tsx files after saving.

You can do this by pressing Strg + Shift + B and select to watch the tsconfig
