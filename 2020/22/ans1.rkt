#lang racket

(define (read-input)
  (let ([deck1 (read-deck)]
        [deck2 (read-deck)])
    (cons deck1 deck2)))

(define (read-deck)
  (do ([_ (read-line)]
       [line (read-line) (read-line)]
       [cards '() (cons (string->number line) cards)])
    ((not (non-empty-string? line)) (reverse cards))))

(define (single-round h1 h2 t1 t2)
  (if (> h1 h2)
      (list (append t1 (list h1 h2)) t2)
      (list t1 (append t2 (list h2 h1)))))

(define (simulate-rounds d1 d2)
  (match (cons d1 d2)
    [(cons '()  _ ) d2]
    [(cons  _  '()) d1]
    [(cons (list h1 t1 ...) (list h2 t2 ...))
      (apply simulate-rounds (single-round h1 h2 t1 t2))]))

(define (calc-score d)
  (let loop ([cs d][n (length d)])
    (if (= n 0)
        0
        (begin
          (printf "~a * ~a~n" n (car cs))
          (+ (* n (car cs)) (loop (cdr cs) (sub1 n)))))))

(define (main)
  (match (read-input)
    [(cons d1 d2) (printf "score=~a~n" (calc-score (simulate-rounds d1 d2)))]))

(main)