#lang racket

(require racket/generator)

; output: HashMap ID (Vec (Vec char))
(define (parse-input)
  (do ([tile (read-tile) (read-tile)]
       [hm (make-hash)])
    ((eof-object? tile) hm)
    (match-let ([`(,tid . ,body) tile])
      (hash-set! hm tid body))))

(define (read-tile)
  (match (read-line)
    [(regexp #px"^Tile (\\d+):" (list _ tid)) (cons tid (read-tile-body))]
    [eof eof]))

(define (read-tile-body)
  (do ([line (read-line) (read-line)]
       [m (make-vector 10)]
       [row 0 (+ row 1)])
    ((or (eof-object? line) (not (non-empty-string? line))) m)
    (vector-set! m row line)))

(define (tile-ref tile row col)
  (string-ref (vector-ref tile row) col))

; input: HashMap ID (Vec (Vec char))
; output: HashMap (Pair Int Int) (Pair ID position-pose)
(define (find-answer tiles)
  (find-answer1 tiles #hash(((0 . 0) . ((sequence-ref (in-hash-keys tiles) 0) . 0)))))

(define (find-answer1 tiles p-ans)
  (if (check-answer-valid tiles p-ans)
      p-ans
      (call/cc
        (λ (return)
          (for ([(tid coord pos) (in-producer (iter-next-tile tiles p-ans) 'done)])
            (let ([try-ans (find-answer1 tiles (hash-set p-ans coord `(,tid . ,pos)))])
              (when try-ans
                (return try-ans))))
          #f))))

(define (check-answer-valid tiles ans)
  (equal? (hash-count tiles) (hash-count ans)))

(define (iter-next-tile tiles p-ans)
  (generator ()
    (for ([(tid tile) (in-hash tiles)]
          #:when (not (hash-has-key? p-ans tid)))
      )))

(define (select-coord m s f)
  (sequence-fold f 0 (sequence-map s (in-hash-keys m))))

(define (left-up m)
  (hash-ref m (cons (select-coord m car min) (select-coord m cdr max))))

(define (right-up m)
  (hash-ref m (cons (select-coord m car max) (select-coord m cdr max))))

(define (left-down m)
  (hash-ref m (cons (select-coord m car min) (select-coord m cdr min))))

(define (right-down m)
  (hash-ref m (cons (select-coord m car max) (select-coord m cdr min))))

(define (prod-corners matrix)
  (apply * (map (λ (f) (string->number (car (f matrix))))
                (list left-up right-up left-down right-down))))

(define (main)
  (let* ([tiles (with-input-from-file "input1" parse-input)]
         [answer (find-answer tiles)])
    (printf "product = ~a" (prod-corners answer))))

(main)

