# Functional patterns in javascript - draft


## A simple range() expression/function

```js
range = (len => [...Array(len).keys()])
range(3)
> [0, 1, 2]
range(10)
> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

Uses the spread operator and Array.prototype.keys()

## factorial one-liner
```js
fac = x => x === 0 ? 1 : x * fac(x-1)
```

Use:
```fac(5)
//> 120```

Author: DJ Adams