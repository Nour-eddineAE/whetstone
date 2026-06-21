// React + htm from CDN (ESM). htm lets us write components with tagged-template
// markup -- no JSX, no build step. One import point so every component shares
// the same React instance.
import React from "https://esm.sh/react@18.2.0";
import * as ReactDOMClient from "https://esm.sh/react-dom@18.2.0/client";
import htm from "https://esm.sh/htm@3.1.1";

// Map htm's fragment shorthand (`<>...</>`, type === null) onto React.Fragment;
// React.createElement rejects a null type otherwise.
const h = (type, props, ...children) =>
  React.createElement(type ? type : React.Fragment, props, ...children);

export const html = htm.bind(h);
export const { useState, useEffect, useMemo, useRef, useCallback } = React;
export { React, ReactDOMClient };
