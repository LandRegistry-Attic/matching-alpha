#!/bin/bash

createuser -s matching
createdb -U matching -O matching matching -T template0
