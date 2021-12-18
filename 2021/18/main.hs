import Text.ParserCombinators.Parsec
import Data.Maybe (fromMaybe)
import System.IO
import System.Environment
import Data.List

data SFNum = Regular Int | Pair SFNum SFNum

instance Show SFNum where
    show (Regular n) = show n
    show (Pair l r)  = "[" ++ show l ++ ", " ++ show r ++ "]"

sfnumListParser :: GenParser Char st [SFNum]
sfnumListParser = 
    do  result <- many (sfnumParser <* spaces)
        eof
        return result

sfnumParser :: GenParser Char st SFNum
sfnumParser = regularParser <|> pairParser

regularParser :: GenParser Char st SFNum
regularParser = Regular . read <$> many1 digit

pairParser :: GenParser Char st SFNum
pairParser = between (char '[') (char ']') pairParserInner


pairParserInner :: GenParser Char st SFNum
pairParserInner =
    do  l <- sfnumParser
        spaces
        char ','
        spaces
        r <- sfnumParser
        return (Pair l r)

add :: SFNum -> SFNum -> SFNum
add x y = reduce (Pair x y)

reduce :: SFNum -> SFNum
reduce n =
    let (n1, r) = explode n 0 in
        if r == NotReduce then
            let (n2, splited) = split n in
                if not splited then
                    n
                else
                    reduce n2
        else
            reduce n1

data ReduceStatus = NotReduce
                  | NeedAddL Int
                  | NeedAddR Int
                  | NeedAddLR Int Int
                  | ReduceDown
                  deriving (Show, Eq)

explode :: SFNum -> Int -> (SFNum, ReduceStatus)
explode n@(Regular _) _ = (n, NotReduce)
explode (Pair (Regular l) (Regular r)) lvl | lvl >= 4 = (Regular 0, NeedAddLR l r)
explode p@(Pair l r) lvl =
    case rsl of
        NotReduce ->
            case rsr of
                NotReduce       -> (p, NotReduce)
                NeedAddR ar     -> (Pair l r1, rsr)
                ReduceDown      -> (Pair l r1, rsr)
                NeedAddL al     -> (Pair (addL l al) r1, ReduceDown)
                NeedAddLR al ar -> (Pair (addL l al) r1, NeedAddR ar)
        NeedAddL al     -> (Pair l1 r, rsl)
        ReduceDown      -> (Pair l1 r, rsl)
        NeedAddR ar     -> (Pair l1 (addR r ar), ReduceDown)
        NeedAddLR al ar -> (Pair l1 (addR r ar), NeedAddL al)
    where (l1, rsl) = explode l (succ lvl)
          (r1, rsr) = explode r (succ lvl)

addL :: SFNum -> Int -> SFNum
addL (Regular n) a = Regular $ n + a
addL (Pair l r) a = Pair l $ addL r a

addR :: SFNum -> Int -> SFNum
addR (Regular n) a = Regular $ n + a
addR (Pair l r) a = Pair (addR l a) r

split :: SFNum -> (SFNum, Bool)
split (Regular n) | n < 10 = (Regular n, False)
                  | n `mod` 2 == 1 = (Pair (Regular $ n `div` 2) (Regular $ n `div` 2 + 1), True)
                  | otherwise      = (Pair (Regular $ n `div` 2) (Regular $ n `div` 2), True)
split (Pair l r) = if el1 then (Pair l1 r, el1) else (Pair l r1, er1)
                   where (l1, el1) = split l
                         (r1, er1) = split r

magnitude :: SFNum -> Int
magnitude (Regular n) = n
magnitude (Pair l r) = (magnitude l) * 3 + (magnitude r) * 2

maxSum2 :: [SFNum] -> Int
maxSum2 ns = maximum [ magnitude (add (ns!!i) (ns!!j)) | i <- indices, j <- indices, i /= j ]
             where indices = [0..(length ns - 1)]

processFile :: String -> IO ()
processFile fileName = parseFromFile sfnumListParser fileName >>= either report myShow
  where
    report err = do
        hPutStrLn stderr $ show err
    myShow es =
        do
            let mysum = foldl1 add es
            print mysum
            print (magnitude mysum)
            print (maxSum2 es)

main = do
    args <- getArgs
    let inputFileName = args !! 0
    processFile inputFileName
