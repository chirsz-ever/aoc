#lang racket

(define-namespace-anchor a)
(define ns (namespace-anchor->namespace a))

(define (parse-expr str)
  (let ((i (open-input-string str)))
    (do ((syms '() (append syms (list s)))
         (s (read i) (read i)))
      ((eof-object? s) syms))))
       

(define (eval-expr e)
  (match e
    [(list lhs op rhs tails ...)
     (eval-expr (cons ((eval op ns) (eval-expr lhs) (eval-expr rhs)) tails))]
    [(list num) #:when (number? num) num]
    [e #:when (number? e) e]))

(define sum-results 0)

(do ((line (read-line) (read-line)))
  ((eof-object? line))
  (let [(result (eval-expr (parse-expr line)))]
    (set! sum-results (+ sum-results result)))
  ;(display result)
  ;(newline)
  )

(display sum-results)
(newline)

