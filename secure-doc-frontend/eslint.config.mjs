import js from "@eslint/js";
import tseslint from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";
import react from "eslint-plugin-react";

export default [
  js.configs.recommended,
  {
    files: ["**/*.ts", "**/*.tsx"],
    languageOptions: {
      parser: tsParser,
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        window: "readonly",
        document: "readonly",
        console: "readonly",
        alert: "readonly",
        localStorage: "readonly",
        process: "readonly",
        test: "readonly",
        expect: "readonly",
        jest: "readonly",
        File: "readonly",
        HTMLInputElement: "readonly",
        FormData: "readonly",
        HTMLElement: "readonly"  
      }
    },
    plugins: {
      "@typescript-eslint": tseslint,
      "react": react
    },
    rules: {
      "no-unused-vars": "warn",
      "react/prop-types": "off"
    }
  }
];
