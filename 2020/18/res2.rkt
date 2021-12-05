#lang racket

(define-namespace-anchor a)
(define ns (namespace-anchor->namespace a))

(define (parse-expr str)
  (let ((i (open-input-string str)))
    (do ((syms '() (append syms (list s)))
         (s (read i) (read i)))
      ((eof-object? s) syms))))

(define (eval-tri op lhs rhs)
  ((eval op ns) (eval-expr lhs) (eval-expr rhs)))

(define (priority op)
  (case op
    [(+) 20]
    [(*) 10]))

(define (pop-stack ops nums prio)
  (if (or (empty? ops) (> prio (priority (car ops))))
      (values ops nums)
      (let ((r (eval-tri (car ops) (cadr nums) (car nums))))
        (pop-stack (cdr ops) (cons r (cddr nums)) prio))))

(define (eval-infix es ops nums)
  (match es
    ['() (let-values ([(_ nums) (pop-stack ops nums 0)]) (car nums))]
    [(list n t ...) #:when (number? n) (eval-infix t ops (cons n nums))]
    [(list sube t ...) #:when (list? sube)
                       (eval-infix t ops (cons (eval-expr sube) nums))]
    [(list op t ...)
     ;(display "op: ")(display op)(newline)
     (let-values ([(ops nums) (pop-stack ops nums (priority op))])
       (eval-infix t (cons op ops) nums))]))

(define (eval-expr e)
  (cond [(list? e) (eval-infix e '() '())]
        [(number? e) e]))

(define sum-results 0)

(do ((line (read-line) (read-line)))
  ((eof-object? line))
  (let [(result (eval-expr (parse-expr line)))]
    (set! sum-results (+ sum-results result))
;    (display result)
;    (newline)
    ))

(display sum-results)
(newline)

