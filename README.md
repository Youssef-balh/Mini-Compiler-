# Moroccan Proverbs Compilation 

## Overview

This project aims to compile a collection of Moroccan proverbs along with their contexts and translations in French and English. Additionally, a chatbot is implemented to correct users when entering proverbs and provide feedback on lexical, syntactic, and semantic errors.

### Structure

#### Proverbs and Contexts

The `proverbs_contexts` dictionary in the code contains Moroccan proverbs as keys and their respective contexts as values. These proverbs are expressions widely used in Moroccan culture, reflecting wisdom, cultural nuances, and life lessons.

#### Translations

Translations of the proverbs are provided in French (`french_data`) and English (`english_data`). Contexts are also translated into French (`french_context`) and English (`english_context`).

#### Photo and Video Data

For a more engaging experience, photo data (`photo_data`) is associated with each proverb, providing visual representations. Users can replace the file paths or URLs with actual media resources.

#### Lexical, Syntactic, and Semantic Analysis

The project utilizes lexer and parser components to perform lexical, syntactic, and semantic analysis on the entered proverbs. The tokens define the lexical units, and the lexer (`lex`) and parser (`yacc`) are implemented to handle the syntax. The code checks for errors during lexing and parsing and provides meaningful feedback.

#### Chatbot Functionality

The chatbot (`chatbot_parser`) is designed to correct users when entering proverbs. It checks for errors in lexical, syntactic, and semantic aspects, providing users with informative messages about any mistakes made.
