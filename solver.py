import argparse
import numpy as np

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Linear system solver: solve Ax + b = y")
    parser.add_argument('--no-bias', action='store_true', help='solve for Ax = y')
    parser.add_argument('--delimiter', type=str, default='\t')
    parser.add_argument('--plot', type=str, help='file to save plot image')
    parser.add_argument('--pred', type=str, help='file to save predictions')
    parser.add_argument('--dtype', choices=['float32', 'float64'], default='float64')
    parser.add_argument('A', type=str, help='file for matrix A')
    parser.add_argument('y', type=str, help='file for vector y')

    args = parser.parse_args()
    A = np.loadtxt(args.A, args.dtype)
    y = np.loadtxt(args.y, args.dtype)
    assert len(A.shape) == 2, "A must be mxn matrix"
    assert len(y.shape) == 1, "y must be m-dim vector"
    assert len(A) == len(y), "dimension mismatch between A and y"

    if not args.no_bias:
        A = np.column_stack([A, np.ones_like(y)])
    
    x, err, _, _ = np.linalg.lstsq(A, y, rcond=None)
    if args.no_bias:
        print(f'x = {x}, err = {err.item()}')
    else:
        print(f'x = {x[:-1]}, b = {x[-1].item()}, err = {err.item()}')
    
    pred = A @ x
    if args.plot:
        import matplotlib.pyplot as plt
        ymin = np.min([y, pred])
        ymax = np.max([y, pred])
        plt.scatter(y, pred)
        plt.plot([ymin, ymax], [ymin, ymax], 'r')
        plt.xlabel('y')
        plt.ylabel('pred')
        plt.legend(['predictions', 'target'])
        plt.savefig(args.plot)

    if args.pred:
        np.savetxt(args.pred, pred, delimiter=args.delimiter)