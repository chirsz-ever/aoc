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
  (cond
    [(and (<= h1 (length t1)) (<= h2 (length t2)))
      (if (player1-will-win (take t1 h1) (take t2 h2))
          (cons (append t1 (list h1 h2)) t2)
          (cons t1 (append t2 (list h2 h1))))]
    [(> h1 h2) (cons (append t1 (list h1 h2)) t2)]
    [else      (cons t1 (append t2 (list h2 h1)))]))

(define (player1-will-win d1 d2)
  (case (car (simulate-rounds '() d1 d2))
    [(player1) #t]
    [else #f]))

(define (simulate-rounds history d1 d2)
  (if (member (cons d1 d2) history)
      (cons 'player1 d1)
      (match (cons d1 d2)
        [(cons '()  _ ) (cons 'player2 d2)]
        [(cons  _  '()) (cons 'player1 d1)]
        [(cons (list h1 t1 ...) (list h2 t2 ...))
          (let ([ds (single-round h1 h2 t1 t2)])
            (simulate-rounds (cons (cons d1 d2) history) (car ds) (cdr ds)))])))

(define (get-result d1 d2)
  (cdr (simulate-rounds '() d1 d2)))

(define (calc-score d)
  (let loop ([cs d][n (length d)])
    (if (= n 0)
        0
        (begin
          (printf "~a * ~a~n" n (car cs))
          (+ (* n (car cs)) (loop (cdr cs) (sub1 n)))))))

(define (main)
  (match (read-input)
    [(cons d1 d2) (printf "score=~a~n" (calc-score (get-result d1 d2)))]))

(main)