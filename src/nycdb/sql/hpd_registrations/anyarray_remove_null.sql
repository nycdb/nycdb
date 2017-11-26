DROP FUNCTION IF EXISTS anyarray_remove_null(anyarray);
CREATE OR REPLACE FUNCTION anyarray_remove_null(from_array anyarray)
        RETURNS anyarray AS
$BODY$
        DECLARE
                -- The variable used to track iteration over "from_array".
                loop_offset integer;

                -- The array to be returned by this function.
                return_array from_array%TYPE;
        BEGIN
                -- Iterate over each element in "from_array".
                FOR loop_offset IN ARRAY_LOWER(from_array, 1)..ARRAY_UPPER(from_array, 1) LOOP
                        IF from_array[loop_offset] IS NOT NULL THEN -- If NULL, will omit from "return_array".
                                return_array = ARRAY_APPEND(return_array, from_array[loop_offset]);
                        END IF;
                END LOOP;

                RETURN return_array;
        END;
$BODY$ LANGUAGE plpgsql;

-- THIS FILE's LICENSE
-- The MIT License (MIT)

-- Copyright © 2013-2014 Joshua D. Burns (JDBurnZ) and Message In Action LLC

-- Joshua D. Burns

-- * https://github.com/JDBurnZ
-- * http://www.joshburns.me


-- Message In Action

-- * https://www.messageinaction.com

-- Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

-- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

-- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
