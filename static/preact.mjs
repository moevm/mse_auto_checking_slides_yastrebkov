import { h, Component, render, createContext, createRef } from 'https://unpkg.com/preact@latest?module';
import { useContext } from 'https://unpkg.com/preact@latest/hooks/dist/hooks.module.js?module';
import htm from 'https://unpkg.com/htm?module';

const html = htm.bind(h); // Initialize htm with Preact

export {Component, render, createContext, createRef, html, useContext};