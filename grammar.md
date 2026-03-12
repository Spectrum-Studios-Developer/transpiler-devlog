$$
\begin{align}

[\text{program}] &\to [\text{statement}]^* \\\\

[\text{statement}] &\to [\text{exit}] \\
                  &| [\text{let}] \\
                  &| [\text{func}] \\
                  &| [\text{return}] \\
                  &| [\text{call}] \\
                  &| [\text{log}] \\
                  &| [\text{if}] \\\\

[\text{exit}] &\to exit([\text{expr}]); \\

[\text{let}] &\to let\ \text{IDENTIFIER} = [\text{expr}]; \\

[\text{func}] &\to func\ \text{IDENTIFIER}([\text{parameters}])\ \{[\text{statement}]^*\} \\

[\text{return}] &\to return\ [\text{expr}]; \\

[\text{call}] &\to call\ \text{IDENTIFIER}([\text{arguments}]); \\

[\text{log}] &\to log([\text{expr}]); \\

[\text{if}] &\to if([\text{expr}])\ \{[\text{statement}]^*\} \\\\

[\text{parameters}] &\to \epsilon \\
                    &| \text{IDENTIFIER} \\
                    &| \text{IDENTIFIER},\ [\text{parameters}] \\\\

[\text{arguments}] &\to \epsilon \\
                   &| [\text{expr}] \\
                   &| [\text{expr}],\ [\text{arguments}] \\

[\text{expr}] &\to [\text{primary}] \\
              &| [\text{expr}]\ +\ [\text{expr}] \\
              &| [\text{expr}]\ -\ [\text{expr}] \\
              &| [\text{expr}]\ *\ [\text{expr}] \\
              &| [\text{expr}]\ /\ [\text{expr}] \\
              &| [\text{expr}]\ ==\ [\text{expr}] \\
              &| [\text{expr}]\ !=\ [\text{expr}] \\
              &| [\text{expr}]\ <\ [\text{expr}] \\
              &| [\text{expr}]\ >\ [\text{expr}] \\

[\text{primary}] &\to \text{NUMBER} \\
                 &| \text{STRING} \\
                 &| \text{IDENTIFIER} \\
                 &| [\text{call\_expr}] \\
                 &| ([\text{expr}]) \\

[\text{call\_expr}] &\to \text{IDENTIFIER}([\text{arguments}])

\end{align}
$$
