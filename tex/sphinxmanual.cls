%
% sphinxmanual.cls for Sphinx (http://sphinx-doc.org/)
%

\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{sphinxmanual}[2017/03/26 v1.5.4 Document class (Sphinx manual)]

% chapters starting at odd pages (overridden by 'openany' document option)
\PassOptionsToClass{openright}{\sphinxdocclass}

% 'oneside' option overriding the 'twoside' default
\newif\if@oneside
\DeclareOption{oneside}{\@onesidetrue}
% Pass remaining document options to the parent class.
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{\sphinxdocclass}}
\ProcessOptions\relax

% Defaults two-side document
\if@oneside
% nothing to do (oneside is the default)
\else
\PassOptionsToClass{twoside}{\sphinxdocclass}
\fi

\LoadClass{\sphinxdocclass}

% Set some sane defaults for section numbering depth and TOC depth.  You can
% reset these counters in your preamble.
%
\setcounter{secnumdepth}{2}
\setcounter{tocdepth}{1}

\newcommand{\blank}[1]{\hspace*{#1}}
% Change the title page to look a bit better, and fit in with the fncychap
% ``Bjarne'' style a bit better.
%
\renewcommand{\maketitle}{%
  \let\spx@tempa\relax
  \ifHy@pageanchor\def\spx@tempa{\Hy@pageanchortrue}\fi
  \hypersetup{pageanchor=false}% avoid duplicate destination warnings

  
  \input{front.inc}	
  \input{front_est.inc}	
  \input{decorig.inc}
  \input{abstract.inc}
  \input{abstract_est.inc}

  %\makeglossaries
  %\printglossaries

   	
  \setcounter{footnote}{0}%
  \let\thanks\relax\let\maketitle\relax
  %\gdef\@thanks{}\gdef\@author{}\gdef\@title{}
  \if@openright\cleardoublepage\else\clearpage\fi
  \spx@tempa
}

\newcommand{\sphinxtableofcontents}{%
  \pagenumbering{roman}%
  \pagestyle{plain}%
  \begingroup
    \addtocontents{toc}{\protect\setstretch{0.95}}
    \parskip \z@skip
    \renewcommand{\contentsname}{Contents}
    \singlespacing
    \tableofcontents
    \onehalfspacing
  \endgroup
  % before resetting page counter, let's do the right thing.
   \listoffigures
     \if@openright\cleardoublepage\else\clearpage\fi
  \pagenumbering{arabic}%
  \ifdefined\fancyhf\pagestyle{normal}\fi
}

% This is needed to get the width of the section # area wide enough in the
% library reference.  Doing it here keeps it the same for all the manuals.
%
\renewcommand*\l@section{\@dottedtocline{1}{1.5em}{2.6em}}
\renewcommand*\l@subsection{\@dottedtocline{2}{4.1em}{3.5em}}

% Fix the bibliography environment to add an entry to the Table of
% Contents.
% For a report document class this environment is a chapter.
%
% Note: \phantomsection is required for TeXLive 2009
% http://tex.stackexchange.com/questions/44088/when-do-i-need-to-invoke-phantomsection#comment166081_44091
\newenvironment{sphinxthebibliography}[1]{%
  \if@openright\cleardoublepage\else\clearpage\fi
  \phantomsection
  \begin{thebibliography}{1}%
  \addcontentsline{toc}{chapter}{\bibname}}{\end{thebibliography}}

% Same for the indices.
% The memoir class already does this, so we don't duplicate it in that case.
%
\@ifclassloaded{memoir}
 {\newenvironment{sphinxtheindex}{\begin{theindex}}{\end{theindex}}}
 {\newenvironment{sphinxtheindex}{%
    \if@openright\cleardoublepage\else\clearpage\fi
    \phantomsection
    \begin{theindex}%
    \addcontentsline{toc}{chapter}{\indexname}}{\end{theindex}}}
