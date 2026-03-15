$$
\begin{align}

[\text{program}] &\to [\text{statement}]^* \\\\

[\text{statement}] &\to [\text{exit}] \\
                  &| [\text{let}] \\
                  &| [\text{func}] \\
                  &| [\text{return}] \\
                  &| [\text{call}] \\
                  &| [\text{log}] \\
                  &| [\text{if}] \\
                  &| [\text{while}] \\
                  &| [\text{inc}] \\
                  &| [\text{dbgstmt}] \\\\

[\text{exit}]    &\to exit\ [\text{expr}]; \\

[\text{let}]     &\to let\ \text{IDENTIFIER} = [\text{expr}]; \\

[\text{func}]    &\to func\ \text{IDENTIFIER}([\text{parameters}])\ \{[\text{statement}]^*\} \\

[\text{return}]  &\to return\ [\text{expr}]; \\

[\text{call}]    &\to call\ \text{IDENTIFIER}([\text{arguments}]); \\

[\text{log}]     &\to log\ [\text{expr}]; \\

[\text{if}]      &\to if([\text{expr}])\ \{[\text{statement}]^*\} \\
                 &| \ if([\text{expr}])\ \{[\text{statement}]^*\}\ else\ \{[\text{statement}]^*\} \\
                 &| \ if([\text{expr}])\ \{[\text{statement}]^*\}\ else\ [\text{if}] \\

[\text{while}]   &\to while([\text{expr}])\ \{[\text{statement}]^*\} \\

[\text{inc}]     &\to inc\ \text{IDENTIFIER},\ [\text{expr}]; \\

[\text{dbgstmt}] &\to \#\ \text{IDENTIFIER}; \\\\

[\text{parameters}] &\to \epsilon \\
                    &| \text{IDENTIFIER} \\
                    &| \text{IDENTIFIER},\ [\text{parameters}] \\\\

[\text{arguments}] &\to \epsilon \\
                   &| [\text{expr}] \\
                   &| [\text{expr}],\ [\text{arguments}] \\\\

[\text{expr}] &\to [\text{primary}] \\
              &| [\text{expr}]\ +\ [\text{expr}] \\
              &| [\text{expr}]\ -\ [\text{expr}] \\
              &| [\text{expr}]\ *\ [\text{expr}] \\
              &| [\text{expr}]\ /\ [\text{expr}] \\
              &| [\text{expr}]\ ==\ [\text{expr}] \\
              &| [\text{expr}]\ !=\ [\text{expr}] \\
              &| [\text{expr}]\ <\ [\text{expr}] \\
              &| [\text{expr}]\ >\ [\text{expr}] \\\\

[\text{primary}] &\to \text{NUMBER} \\
                 &| \text{STRING} \\
                 &| \text{IDENTIFIER} \\
                 &| \text{true} \\
                 &| \text{false} \\
                 &| [\text{call\_expr}] \\
                 &| ([\text{expr}]) \\\\

[\text{call\_expr}] &\to \text{IDENTIFIER}([\text{arguments}])

\end{align}
$$